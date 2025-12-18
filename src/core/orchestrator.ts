import { projectState } from './state-manager';
import { ProjectManager } from './agents/pm';
import { UiDesigner } from './agents/ui-designer';
import { FrontendDev } from './agents/frontend';
import { BackendDev } from './agents/backend';
import { ContentWriter } from './agents/writer';
import { CodeReviewer } from './agents/reviewer';
import { QaTester } from './agents/qa';

export class Orchestrator {
  private pm = new ProjectManager();
  private ui = new UiDesigner();
  private frontend = new FrontendDev();
  private backend = new BackendDev();
  private writer = new ContentWriter();
  private reviewer = new CodeReviewer();
  private qa = new QaTester();

  async startProject(userPrompt: string) {
    console.log(\`🚀 Starting Project: "\${userPrompt}"\`);

    // 1. PM
    console.log("--- PHASE 1: Planning ---");
    const brief = await this.pm.analyze(userPrompt);
    await projectState.saveBrief(brief);

    // 2. UI
    console.log("--- PHASE 2: Designing ---");
    const design = await this.ui.createDesign(brief);
    await projectState.saveDesign(design);

    // 3. CODE (Parallel)
    console.log("--- PHASE 3: Coding & Writing ---");
    const [frontendFiles, backendFiles, content] = await Promise.all([
      this.frontend.generateCode(brief, design),
      this.backend.generateAPIs(brief),
      this.writer.writeContent(brief, design)
    ]);

    await projectState.saveFrontendCode(frontendFiles);
    await projectState.saveBackendCode(backendFiles);

    // 4. REVIEW
    console.log("--- PHASE 4: Reviewing ---");
    const review = await this.reviewer.reviewCode(frontendFiles, backendFiles);
    
    // 5. QA
    console.log("--- PHASE 5: Quality Assurance ---");
    const qaReport = await this.qa.test(frontendFiles, backendFiles);

    return {
      status: "SUCCESS",
      message: "Project Completed with 8 Agents!",
      finalState: {
        ...projectState.getState(),
        content,
        review,
        qaReport
      }
    };
  }
}
