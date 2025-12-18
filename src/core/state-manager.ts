import fs from 'fs/promises';
import path from 'path';
import { ProjectState, ProjectBrief, UiDesign, CodeFile } from '@/types';

const DB_FILE = path.join(process.cwd(), 'project-data.json');

export class StateManager {
  private state: ProjectState;

  constructor() {
    this.state = {
      step: 'discovery',
      projectBrief: null,
      uiDesign: null,
      architecture: { frontend: null, backend: null },
      code: { frontend: [], backend: [] },
      content: {},
      qaReport: null
    };
  }

  getState() { return this.state; }

  async saveBrief(brief: ProjectBrief) {
    this.state.projectBrief = brief;
    this.state.step = 'design';
    await this.persist();
  }

  async saveDesign(design: UiDesign) {
    this.state.uiDesign = design;
    this.state.step = 'implementation';
    await this.persist();
  }

  async saveFrontendCode(files: CodeFile[]) {
    this.state.code.frontend = files;
    await this.persist();
  }

  async saveBackendCode(files: CodeFile[]) {
    this.state.code.backend = files;
    await this.persist();
  }

  private async persist() {
    try {
      await fs.writeFile(DB_FILE, JSON.stringify(this.state, null, 2));
      console.log("💾 State saved to project-data.json");
    } catch (error) { console.error("Error saving state:", error); }
  }
}
export const projectState = new StateManager();
