import Link from 'next/link';

export default function HomePage() {
  return (
    <main className="flex flex-1 flex-col justify-center text-center">
      <h1 className="mb-4 text-2xl font-bold">Welcome to YAKE! Documentation website</h1>
      <p className="text-fd-muted-foreground">
        Open{' '}
        <Link
          href="/docs/--home"
          className="text-fd-foreground font-semibold underline"
        >
          /docs/--home
        </Link>{' '}
        and see the documentation.
      </p>
    </main>
  );
}
