import Nav from "@/components/Nav";
import Hero from "@/components/Hero";
import Problem from "@/components/Problem";
import LoopDiagram from "@/components/LoopDiagram";
import Demo from "@/components/Demo";
import Results from "@/components/Results";
import Findings from "@/components/Findings";
import Methodology from "@/components/Methodology";
import Limitations from "@/components/Limitations";
import Footer from "@/components/Footer";

export default function Home() {
  return (
    <>
      <Nav />
      <main id="main">
        <Hero />
        <Problem />
        <LoopDiagram />
        <Demo />
        <Results />
        <Findings />
        <Methodology />
        <Limitations />
        <Footer />
      </main>
    </>
  );
}
