import {
  Award,
  Bot,
  Code,
  Container,
  Flame,
  GitBranch,
  Moon,
  Star,
  Target,
  type LucideIcon,
} from "lucide-react";

const ICONS: Record<string, LucideIcon> = {
  target: Target,
  "git-branch": GitBranch,
  container: Container,
  code: Code,
  flame: Flame,
  bot: Bot,
  star: Star,
  moon: Moon,
};

export function BadgeIcon({ name, className }: { name: string; className?: string }) {
  const Icon = ICONS[name] ?? Award;
  return <Icon className={className} />;
}
