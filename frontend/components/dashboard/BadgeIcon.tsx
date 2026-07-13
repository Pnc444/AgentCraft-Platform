import {
  Award,
  Bot,
  Compass,
  Container,
  Hash,
  Lightbulb,
  MessageSquare,
  Rocket,
  Sparkles,
  Star,
  Target,
  Trophy,
  Zap,
  type LucideIcon,
} from "lucide-react";

const ICONS: Record<string, LucideIcon> = {
  target: Target,
  lightbulb: Lightbulb,
  hash: Hash,
  compass: Compass,
  "message-square": MessageSquare,
  bot: Bot,
  container: Container,
  rocket: Rocket,
  zap: Zap,
  sparkles: Sparkles,
  trophy: Trophy,
  star: Star,
  award: Award,
};

export function BadgeIcon({ name, className }: { name: string; className?: string }) {
  const Icon = ICONS[name] ?? Award;
  return <Icon className={className} />;
}
