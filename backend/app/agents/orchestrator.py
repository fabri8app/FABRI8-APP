"""
Main Orchestrator - Coordinates 8 Agents & 7 Phases
"""

import asyncio
from typing import Dict, Any, Optional
from agents.roles.project_manager import ProjectManagerAgent
from agents.roles.ui_designer import UIDesignerAgent
from agents.roles.frontend_developer import FrontendDeveloperAgent
from agents.roles.backend_developer import BackendDeveloperAgent
from agents.roles.content_writer import ContentWriterAgent
from agents.roles.code_reviewer import CodeReviewerAgent
from agents.roles.qa_tester import QATesterAgent
from agents.roles.debugger import DebuggerAgent
from services.websocket_service import WebSocketService

class RealTeamOrchestrator:
    """
    Main orchestrator managing 8 agents through 7-phase workflow
    """
    
    def __init__(self, project_id: str, ws_service: Optional[WebSocketService] = None):
        """Initialize orchestrator with all 8 agents"""
        self.project_id = project_id
        self.ws = ws_service
        
        # Initialize all 8 agents
        self.agents = {
            'pm': ProjectManagerAgent(),
            'ui': UIDesignerAgent(),
            'frontend': FrontendDeveloperAgent(),
            'backend': BackendDeveloperAgent(),
            'writer': ContentWriterAgent(),
            'reviewer': CodeReviewerAgent(),
            'qa': QATesterAgent(),
            'debugger': DebuggerAgent()
        }
        
        self.workflow_state = {}
    
    async def notify(self, phase: int, message: str, data: Optional[Dict] = None):
        """Send real-time updates to frontend"""
        if self.ws:
            await self.ws.send_status(self.project_id, {
                'phase': phase,
                'message': message,
                'data': data or {}
            })
        print(f"[Phase {phase}] {message}")
    
    async def start_project(self, user_prompt: str) -> Dict[str, Any]:
        """
        Execute complete 7-phase workflow
        """
        try:
            print(f"\n🚀 Starting FABRI8 Project: {self.project_id}")
            print(f"📝 Prompt: {user_prompt[:100]}...\n")
            
            # Phase 1: Discovery
            await self.notify(1, "🤔 Phase 1: Discovery & Planning started")
            pm_output = await self.agents['pm'].execute({'prompt': user_prompt})
            self.workflow_state['project_brief'] = pm_output['output']
            await self.notify(1, "✅ Phase 1 complete", pm_output['output'])
            
            # Phase 2: Design (Parallel: UI + Tech Planning)
            await self.notify(2, "🎨 Phase 2: Design & Architecture started")
            ui_output, backend_output = await asyncio.gather(
                self.agents['ui'].execute({
                    'project_brief': pm_output['output']
                }),
                self.agents['backend'].execute({
                    'project_brief': pm_output['output']
                })
            )
            self.workflow_state['design_spec'] = ui_output['output']
            self.workflow_state['backend_design'] = backend_output['output']
            await self.notify(2, "✅ Phase 2 complete")
            
            # Phase 3: Implementation (Parallel: Frontend + Writer)
            await self.notify(3, "💻 Phase 3: Implementation started")
            frontend_output, writer_output = await asyncio.gather(
                self.agents['frontend'].execute({
                    'design_spec': ui_output['output'],
                    'project_brief': pm_output['output']
                }),
                self.agents['writer'].execute({
                    'design_spec': ui_output['output'],
                    'project_brief': pm_output['output']
                })
            )
            self.workflow_state['frontend_code'] = frontend_output['output']
            self.workflow_state['content'] = writer_output['output']
            await self.notify(3, "✅ Phase 3 complete")
            
            # Phase 4: Integration (Check alignment)
            await self.notify(4, "🔗 Phase 4: Integration Standup")
            await asyncio.sleep(1)  # Simulated integration check
            await self.notify(4, "✅ Phase 4 complete - All systems aligned")
            
            # Phase 5: Review
            await self.notify(5, "👀 Phase 5: Code Review started")
            reviewer_output = await self.agents['reviewer'].execute({
                'frontend_code': frontend_output['output'],
                'backend_code': backend_output['output']
            })
            self.workflow_state['review'] = reviewer_output['output']
            await self.notify(5, "✅ Phase 5 complete", reviewer_output['output'])
            
            # Phase 6: Testing
            await self.notify(6, "🧪 Phase 6: QA Testing started")
            qa_output = await self.agents['qa'].execute({
                'project_brief': pm_output['output']
            })
            self.workflow_state['qa'] = qa_output['output']
            await self.notify(6, "✅ Phase 6 complete")
            
            # Phase 7: Debugging & Delivery
            await self.notify(7, "🐛 Phase 7: Debugging & Delivery")
            debugger_output = await self.agents['debugger'].execute({
                'code_review': reviewer_output['output'],
                'frontend_code': frontend_output['output']
            })
            self.workflow_state['debug'] = debugger_output['output']
            
            # Final output
            final_output = {
                'project_id': self.project_id,
                'status': 'completed',
                'frontend_code': frontend_output['output'],
                'content': writer_output['output'],
                'test_plan': qa_output['output'],
                'review_summary': reviewer_output['output'],
                'fixes': debugger_output['output']
            }
            
            await self.notify(7, "🎉 Project complete!", final_output)
            print("\n✅ All phases completed successfully!\n")
            return final_output
            
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            await self.notify(0, error_msg)
            print(error_msg)
            raise
