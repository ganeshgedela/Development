type Props = {
    onSelect: (index: number) => void;
  };
  
  export default function TraceFileTable({ onSelect }: Props) {
    return (
      <section className="bg-white p-4 rounded shadow-md">
        <div className="flex justify-between items-center mb-2">
          <h3 className="text-lg font-semibold">Network Trace Files</h3>
          <div className="space-x-2">
            <button className="bg-blue-600 text-white px-3 py-1 rounded">Upload</button>
            <button className="bg-red-500 text-white px-3 py-1 rounded">Delete</button>
          </div>
        </div>
        <div className="overflow-x-auto">
          <table className="table-auto w-full text-sm">
            <thead className="bg-gray-200">
              <tr>
                <th className="px-2 py-1 text-left">File Name</th>
                <th className="px-2 py-1 text-left">Timestamp</th>
                <th className="px-2 py-1 text-left">Size</th>
                <th className="px-2 py-1 text-left">Status</th>
                <th className="px-2 py-1 text-left">Actions</th>
              </tr>
            </thead>
          </table>
          <div className="max-h-60 overflow-y-auto">
            <table className="table-auto w-full text-sm">
              <tbody>
                {[...Array(10)].map((_, idx) => (
                  <tr key={idx} className="border-t">
                    <td className="px-2 py-1">trace_{idx}.pcap</td>
                    <td className="px-2 py-1">2025-04-25 10:0{idx}</td>
                    <td className="px-2 py-1">1.2 MB</td>
                    <td className="px-2 py-1">Parsed</td>
                    <td className="px-2 py-1">
                      <button className="text-blue-600" onClick={() => onSelect(idx)}>View</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>
    );
  }
  