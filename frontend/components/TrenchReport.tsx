import ReactMarkdown from 'react-markdown'

interface TrenchReportProps {
  markdown: string
}

export default function TrenchReport({ markdown }: TrenchReportProps) {
  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="border-b border-gray-200 pb-4 mb-4">
        <h2 className="text-lg font-semibold text-gray-900">AI Analysis Report</h2>
        <p className="text-sm text-gray-600 mt-1">Powered by GPT-4</p>
      </div>
      
      <div className="prose prose-sm max-w-none">
        <ReactMarkdown
          components={{
            h1: ({ children }) => <h1 className="text-xl font-bold text-gray-900 mb-3">{children}</h1>,
            h2: ({ children }) => <h2 className="text-lg font-semibold text-gray-900 mb-2 mt-4">{children}</h2>,
            h3: ({ children }) => <h3 className="text-base font-medium text-gray-900 mb-2 mt-3">{children}</h3>,
            p: ({ children }) => <p className="text-gray-700 mb-3 leading-relaxed">{children}</p>,
            ul: ({ children }) => <ul className="list-disc list-inside space-y-1 mb-3 text-gray-700">{children}</ul>,
            ol: ({ children }) => <ol className="list-decimal list-inside space-y-1 mb-3 text-gray-700">{children}</ol>,
            li: ({ children }) => <li className="ml-4">{children}</li>,
            strong: ({ children }) => <strong className="font-semibold text-gray-900">{children}</strong>,
            em: ({ children }) => <em className="italic text-gray-700">{children}</em>,
            blockquote: ({ children }) => (
              <blockquote className="border-l-4 border-blue-500 pl-4 my-3 text-gray-700 italic">
                {children}
              </blockquote>
            ),
            code: ({ children }) => (
              <code className="bg-gray-100 px-1.5 py-0.5 rounded text-sm font-mono text-gray-800">
                {children}
              </code>
            ),
            pre: ({ children }) => (
              <pre className="bg-gray-100 p-3 rounded-lg overflow-x-auto mb-3">
                {children}
              </pre>
            ),
          }}
        >
          {markdown}
        </ReactMarkdown>
      </div>
    </div>
  )
}
