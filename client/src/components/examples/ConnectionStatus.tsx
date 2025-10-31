import { ConnectionStatus } from '../ConnectionStatus';

export default function ConnectionStatusExample() {
  return (
    <div className="flex gap-4">
      <ConnectionStatus isConnected={true} lastUpdate="2s ago" />
      <ConnectionStatus isConnected={false} />
    </div>
  );
}
