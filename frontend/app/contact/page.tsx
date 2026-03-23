import Link from "next/link";
import { ArrowLeft, Mail, MessageSquare, Phone } from "lucide-react";

export default function ContactPage() {
  return (
    <div className="min-h-screen bg-white pt-20">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <Link href="/" className="inline-flex items-center gap-2 text-blue-600 hover:underline mb-8">
          <ArrowLeft size={16} />
          Back to Home
        </Link>

        <h1 className="text-5xl font-bold text-gray-900 mb-6">Contact Us</h1>
        <p className="text-xl text-gray-600 mb-12">
          Have questions about T&P workflow automation? We&apos;re here to help.
        </p>

        <div className="grid md:grid-cols-2 gap-8 mb-12">
          <div className="border border-gray-200 rounded-xl p-6 hover:shadow-md transition-shadow">
            <Mail className="text-blue-600 mb-4" size={32} />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Email Us</h3>
            <p className="text-gray-600 mb-4">Get in touch via email for detailed inquiries</p>
            <a href="mailto:support@corpomailer.com" className="text-blue-600 hover:underline font-medium">
              support@corpomailer.com
            </a>
          </div>

          <div className="border border-gray-200 rounded-xl p-6 hover:shadow-md transition-shadow">
            <MessageSquare className="text-blue-600 mb-4" size={32} />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Live Chat</h3>
            <p className="text-gray-600 mb-4">Chat with our support team in real-time</p>
            <button className="text-blue-600 hover:underline font-medium">
              Start a conversation
            </button>
          </div>
        </div>

        <div className="bg-gray-50 rounded-xl p-8 border border-gray-200">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Send us a message</h2>
          <form className="space-y-6">
            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Name</label>
                <input
                  type="text"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                  placeholder="Your name"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Email</label>
                <input
                  type="email"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                  placeholder="you@example.com"
                />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Subject</label>
              <input
                type="text"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                placeholder="How can we help?"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Message</label>
              <textarea
                rows={6}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none resize-none"
                placeholder="Tell us more about your inquiry..."
              />
            </div>
            <button
              type="submit"
              className="w-full bg-black text-white py-3 px-6 rounded-lg font-medium hover:bg-gray-800 transition-colors"
            >
              Send Message
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
