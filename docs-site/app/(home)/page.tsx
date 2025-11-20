import Link from 'next/link';
import { ArrowRight, Code2, Zap, Globe, BookOpen, Github, FileText } from 'lucide-react';

export default function HomePage() {
  return (
    <main className="flex flex-1 flex-col">
      {/* Hero Section */}
      <section className="relative flex flex-col items-center justify-center px-6 py-24 text-center overflow-hidden">
        
        {/* Content */}
        <div className="max-w-4xl mx-auto space-y-8">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 text-sm font-medium border border-blue-200 dark:border-blue-800">
            <Zap className="w-4 h-4" />
            <span>Unsupervised Keyword Extraction</span>
          </div>

          {/* Title */}
          <h1 className="text-5xl md:text-7xl font-bold bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 dark:from-blue-400 dark:via-indigo-400 dark:to-purple-400 bg-clip-text text-transparent">
            YAKE!
          </h1>
          
          <p className="text-xl md:text-2xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
            Yet Another Keyword Extractor
          </p>
          
          <p className="text-lg text-gray-500 dark:text-gray-400 max-w-3xl mx-auto leading-relaxed">
            A light-weight unsupervised automatic keyword extraction method using text statistical features. 
            No training required. Language-independent. Single-document processing.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center pt-4">
            <Link
              href="/docs/-getting-started"
              className="group inline-flex items-center gap-2 px-8 py-4 rounded-lg bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-semibold shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-105"
            >
              Get Started
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </Link>
            
            <Link
              href="/docs/--home"
              className="inline-flex items-center gap-2 px-8 py-4 rounded-lg bg-white dark:bg-gray-800 border-2 border-gray-200 dark:border-gray-700 hover:border-blue-500 dark:hover:border-blue-500 text-gray-700 dark:text-gray-200 font-semibold transition-all duration-200 hover:shadow-lg"
            >
              <BookOpen className="w-5 h-5" />
              Documentation
            </Link>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 pt-12 max-w-3xl mx-auto">
            <div className="space-y-1">
              <div className="text-3xl font-bold text-blue-600 dark:text-blue-400">25+</div>
              <div className="text-sm text-gray-500 dark:text-gray-400">Languages</div>
            </div>
            <div className="space-y-1">
              <div className="text-3xl font-bold text-indigo-600 dark:text-indigo-400">500+</div>
              <div className="text-sm text-gray-500 dark:text-gray-400">Citations</div>
            </div>
            <div className="space-y-1">
              <div className="text-3xl font-bold text-purple-600 dark:text-purple-400">8M+</div>
              <div className="text-sm text-gray-500 dark:text-gray-400">Downloads</div>
            </div>
            <div className="space-y-1">
              <div className="text-3xl font-bold text-pink-600 dark:text-pink-400">Open</div>
              <div className="text-sm text-gray-500 dark:text-gray-400">Source</div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="px-6 py-20 bg-white dark:bg-gray-900">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-4">
            Why Choose YAKE?
          </h2>
          <p className="text-center text-gray-500 dark:text-gray-400 mb-16 max-w-2xl mx-auto">
            Powerful features that make keyword extraction simple and effective
          </p>
          
          <div className="grid md:grid-cols-3 gap-8">
            {/* Feature 1 */}
            <div className="group p-8 rounded-2xl bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-950/30 dark:to-indigo-950/30 border border-blue-100 dark:border-blue-900/50 hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
              <div className="w-14 h-14 rounded-lg bg-gradient-to-br from-blue-500 to-indigo-500 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <Zap className="w-7 h-7 text-white" />
              </div>
              <h3 className="text-xl font-bold mb-3 text-gray-900 dark:text-white">
                Unsupervised
              </h3>
              <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                No training required. Works out-of-the-box without the need for labeled data or external corpora.
              </p>
            </div>

            {/* Feature 2 */}
            <div className="group p-8 rounded-2xl bg-gradient-to-br from-purple-50 to-pink-50 dark:from-purple-950/30 dark:to-pink-950/30 border border-purple-100 dark:border-purple-900/50 hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
              <div className="w-14 h-14 rounded-lg bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <Globe className="w-7 h-7 text-white" />
              </div>
              <h3 className="text-xl font-bold mb-3 text-gray-900 dark:text-white">
                Language Independent
              </h3>
              <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                Supports 25+ languages without language-specific configurations or dictionaries.
              </p>
            </div>

            {/* Feature 3 */}
            <div className="group p-8 rounded-2xl bg-gradient-to-br from-green-50 to-emerald-50 dark:from-green-950/30 dark:to-emerald-950/30 border border-green-100 dark:border-green-900/50 hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
              <div className="w-14 h-14 rounded-lg bg-gradient-to-br from-green-500 to-emerald-500 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <FileText className="w-7 h-7 text-white" />
              </div>
              <h3 className="text-xl font-bold mb-3 text-gray-900 dark:text-white">
                Single Document
              </h3>
              <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                Extracts keywords from individual documents. No corpus needed for comparison.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Quick Start Section */}
      <section className="px-6 py-20 bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-800 dark:to-gray-900">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-4">
            Quick Start
          </h2>
          <p className="text-center text-gray-500 dark:text-gray-400 mb-12">
            Get started with YAKE in seconds
          </p>
          
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl p-8 border border-gray-200 dark:border-gray-700">
            <div className="flex items-center gap-3 mb-6 pb-4 border-b border-gray-200 dark:border-gray-700">
              <Code2 className="w-6 h-6 text-blue-500" />
              <span className="font-semibold text-gray-700 dark:text-gray-200">Installation</span>
            </div>
            
            <div className="space-y-6">
              <div>
                <div className="text-sm text-gray-500 dark:text-gray-400 mb-2">Install via pip:</div>
                <pre className="bg-gray-900 dark:bg-gray-950 text-gray-100 p-4 rounded-lg overflow-x-auto">
                  <code>pip install git+https://github.com/LIAAD/yake</code>
                </pre>
              </div>
              
              <div>
                <div className="text-sm text-gray-500 dark:text-gray-400 mb-2">Basic usage:</div>
                <pre className="bg-gray-900 dark:bg-gray-950 text-gray-100 p-4 rounded-lg overflow-x-auto text-sm">
                  <code>{`import yake

text = "Your text here..."
kw_extractor = yake.KeywordExtractor()
keywords = kw_extractor.extract_keywords(text)

for kw, score in keywords:
    print(f"{kw}: {score:.4f}")`}</code>
                </pre>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Links Section */}
      <section className="px-6 py-16 bg-white dark:bg-gray-900">
        <div className="max-w-4xl mx-auto">
          <div className="grid md:grid-cols-2 gap-6">
            <Link
              href="https://github.com/LIAAD/yake"
              target="_blank"
              className="group flex items-center gap-4 p-6 rounded-xl border-2 border-gray-200 dark:border-gray-700 hover:border-blue-500 dark:hover:border-blue-500 transition-all duration-200 hover:shadow-lg"
            >
              <Github className="w-12 h-12 text-gray-700 dark:text-gray-300 group-hover:text-blue-500 transition-colors" />
              <div>
                <h3 className="font-bold text-lg mb-1">GitHub Repository</h3>
                <p className="text-sm text-gray-500 dark:text-gray-400">View source code and contribute</p>
              </div>
              <ArrowRight className="w-5 h-5 ml-auto text-gray-400 group-hover:text-blue-500 group-hover:translate-x-1 transition-all" />
            </Link>

            <Link
              href="https://colab.research.google.com/github/tiagolv/yakerf/blob/gh-pages/1YAKE.ipynb"
              target="_blank"
              className="group flex items-center gap-4 p-6 rounded-xl border-2 border-gray-200 dark:border-gray-700 hover:border-orange-500 dark:hover:border-orange-500 transition-all duration-200 hover:shadow-lg"
            >
              <div className="w-12 h-12 rounded-lg bg-orange-500 flex items-center justify-center">
                <Code2 className="w-6 h-6 text-white" />
              </div>
              <div>
                <h3 className="font-bold text-lg mb-1">Try on Colab</h3>
                <p className="text-sm text-gray-500 dark:text-gray-400">Interactive Python notebook</p>
              </div>
              <ArrowRight className="w-5 h-5 ml-auto text-gray-400 group-hover:text-orange-500 group-hover:translate-x-1 transition-all" />
            </Link>
          </div>
        </div>
      </section>
    </main>
  );
}
