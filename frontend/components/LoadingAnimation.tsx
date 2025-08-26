export default function LoadingAnimation() {
  return (
    <div className="flex justify-center items-center py-16">
      <div className="text-center">
        {/* Simple spinner */}
        <div className="inline-flex relative mb-4">
          <div className="w-12 h-12 border-4 border-gray-200 rounded-full"></div>
          <div className="w-12 h-12 border-4 border-transparent border-t-blue-600 rounded-full animate-spin absolute top-0 left-0"></div>
        </div>
        
        {/* Clean text */}
        <p className="text-gray-700 font-medium">Analyzing Token</p>
        <p className="text-gray-500 text-sm mt-1">Please wait a moment...</p>
      </div>
    </div>
  )
}