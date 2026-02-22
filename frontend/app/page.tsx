import Hero from "@/components/Hero";
import BentoGrid from "@/components/BentoGrid";
import FeatureDetails from "@/components/FeatureDetails";
import Link from "next/link";

export default function Home() {
  return (
    <>
      <Hero />
      <BentoGrid />
      <FeatureDetails />

      <section className="mt-16 py-24 bg-black text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-5xl font-bold mb-8 tracking-tight">
            Ready to streamline your <br /> placement outreach?
          </h2>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/dashboard"
              className="bg-white text-black px-8 py-4 rounded-full font-bold text-lg hover:bg-gray-200 transition-colors"
            >
              Open Dashboard
            </Link>
            <Link
              href="/admin"
              className="bg-transparent border border-gray-700 text-white px-8 py-4 rounded-full font-bold text-lg hover:border-white transition-colors"
            >
              Admin Console
            </Link>
          </div>
        </div>
      </section>
    </>
  );
}
