import { redirect } from "next/navigation";

/** Settings lives on the profile page tabs. */
export default function SettingsPage() {
  redirect("/dashboard/profile?tab=settings");
}
