import { useState } from "react";
import Header from "./components/Header";
import TraceFileTable from "./components/NetworkTraceFileTable";
import SelectedFileTabs from "./components/SelectedFileTabs";
import DeploymentSummary from "./components/DeploymentSummary";

export default function App() {
  const [selectedFile, setSelectedFile] = useState<number | null>(null);

  return (
    <div className="min-h-screen bg-gray-100 p-4 space-y-6">
      <Header />
      <TraceFileTable onSelect={setSelectedFile} />
      {selectedFile !== null && <SelectedFileTabs selectedFile={selectedFile} />}
      <DeploymentSummary />
    </div>
  );
}
