import type { StatusItem } from "@/lib/artifacts";

export function StatusRail({ statusItems }: { statusItems: StatusItem[] }) {
  return (
    <div className="status-rail">
      <div className="rail-header">
        <p className="eyebrow dark">Trace</p>
        <h2>Agent Activity</h2>
      </div>
      {statusItems.length === 0 ? (
        <p className="empty-copy">No agent activity yet.</p>
      ) : (
        <ol className="status-list">
          {statusItems.map((item) => (
            <li key={item.id}>
              <span className={`status-marker ${item.state}`} />
              <div>
                <p>{item.label}</p>
                <span>{item.state}</span>
              </div>
            </li>
          ))}
        </ol>
      )}
    </div>
  );
}
