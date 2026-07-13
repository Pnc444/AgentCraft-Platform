import { redirect } from "next/navigation";

export default function LessonIndexPage({
  params,
}: {
  params: { slug: string; lessonSlug: string };
}) {
  redirect(`/dashboard/courses/${params.slug}/lessons/${params.lessonSlug}/content`);
}
