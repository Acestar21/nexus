interface ProviderStatusProps {
    name: string;
    online: boolean;
    last_fetched: string | null;
    error: string | null;
}

export function ProviderStatus({ name, online, last_fetched, error }: ProviderStatusProps) {
    const formatTime = (iso: string) => {
        const date = new Date(iso);
        const now = new Date();
        const diffMs = now.getTime() - date.getTime();
        const diffMins = Math.floor(diffMs / 60000);
        
        if (diffMins < 1) return "just now";
        if (diffMins < 60) return `${diffMins}m ago`;
        const diffHours = Math.floor(diffMins / 60);
        if (diffHours < 24) return `${diffHours}h ago`;
        const diffDays = Math.floor(diffHours / 24);
        return `${diffDays}d ago`;
    };

    return (
        <div className="provider-status">
            <div className="status-header">
                <span className="status-name">{name}</span>
                    <span className={`status-indicator ${online ? "online" : "offline"}`}>
                        { online ? "✓ ONLINE" : "⊘ OFFLINE"}
                </span>
            </div>
            {last_fetched && (
            <div className="status-meta">
                Last updated: {formatTime(last_fetched)}
            </div>
            )}
            {error && (
            <div className="status-error">
                Error: {error.substring(0, 50)}...
            </div>
            )}
        </div>
        );
    }