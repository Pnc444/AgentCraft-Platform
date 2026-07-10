/** Roadmap stage content for the landing page roadmap section. */

export interface RoadmapStage {
  level: number;
  title: string;
  description: string;
  skills: string[];
  checkpoint: string;
  locked: boolean;
}

export const ROADMAP_STAGES: RoadmapStage[] = [
  { level: 1, title: "Start Here", description: "Understand what AI agents are and why they matter.", skills: ["AI agent basics", "Tools & memory", "Prompts & workflows"], checkpoint: "Define what an agent does in your own words", locked: false },
  { level: 2, title: "Programming Foundations", description: "Build the Python skills you need before touching agents.", skills: ["Basic Python", "Functions", "Files", "APIs"], checkpoint: "Call a simple API from a Python script", locked: false },
  { level: 3, title: "Web Basics", description: "Learn how users interact with apps on the web.", skills: ["HTML/CSS/JS", "Frontend structure", "Forms & input"], checkpoint: "Build a simple form that submits data", locked: true },
  { level: 4, title: "Backend Basics", description: "Connect frontend ideas to servers, routes, and data.", skills: ["Django routes", "Databases", "Auth basics", "User accounts"], checkpoint: "Create a login-protected page", locked: true },
  { level: 5, title: "AI Concepts", description: "Understand models, limits, and safe behavior.", skills: ["Prompts", "Context windows", "Model limits", "Safe AI use"], checkpoint: "Write a prompt with clear constraints", locked: true },
  { level: 6, title: "Agent Tools", description: "Give agents limited, scoped abilities.", skills: ["Tool calling", "Search", "File handling", "Scoped actions"], checkpoint: "Wire one tool to a small assistant", locked: true },
  { level: 7, title: "Build an Agent", description: "Create a small working AI assistant with a defined purpose.", skills: ["Purpose design", "Tool connection", "Behavior testing"], checkpoint: "Ship a working mini-assistant", locked: true },
  { level: 8, title: "Capstone Project", description: "Build a complete project and show your progress.", skills: ["End-to-end build", "Portfolio piece", "Deployment basics"], checkpoint: "Deploy and demo your capstone", locked: true },
  { level: 9, title: "Portfolio Ready", description: "Polish, deploy, and showcase what you built.", skills: ["Final polish", "Deployment", "Resume showcase"], checkpoint: "Publish your project story", locked: true },
];
