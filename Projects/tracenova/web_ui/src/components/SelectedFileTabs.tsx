type Props = {
    selectedFile: number;
  };
  
  export default function SelectedFileTabs({ selectedFile }: Props) {
    return (
      <section className="bg-white p-4 rounded shadow-md">
        <h3 className="text-lg font-semibold mb-2">Selected File: trace_{selectedFile}.pcap</h3>
        <div className="border-b mb-3">
          <nav className="flex gap-4 text-blue-600">
            <button className="font-semibold">SIP</button>
            <button>Diameter</button>
            <button>NAS</button>
            <button>NGAP</button>
          </nav>
        </div>
        <div className="overflow-x-auto">
          <table className="table-auto w-full text-sm">
            <thead className="bg-gray-200">
              <tr>
                <th className="px-2 py-1 text-left">Timestamp</th>
                <th className="px-2 py-1 text-left">Source</th>
                <th className="px-2 py-1 text-left">Destination</th>
                <th className="px-2 py-1 text-left">Protocol</th>
                <th className="px-2 py-1 text-left">Message</th>
              </tr>
            </thead>
          </table>
          <div className="max-h-60 overflow-y-auto">
            <table className="table-auto w-full text-sm">
              <tbody>
                {[...Array(10)].map((_, idx) => (
                  <tr key={idx} className="border-t">
                    <td className="px-2 py-1">2025-04-25 10:{idx}0</td>
                    <td className="px-2 py-1">192.168.1.1</td>
                    <td className="px-2 py-1">10.0.0.1</td>
                    <td className="px-2 py-1">SIP</td>
                    <td className="px-2 py-1">INVITE</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>
    );
  }
  