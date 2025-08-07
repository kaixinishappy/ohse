import Link from "next/link";

export default function Home() {
  return (
    <div style={{ padding: 30 }}>
      <h1>Welcome</h1>
      <Link href="/reporting-form">Go to Reporting Form →</Link>
    </div>
  );
}
