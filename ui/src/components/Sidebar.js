import React from "react";

const Sidebar = () => {
  const onDragStart = (event, nodeType , label) => {
    event.dataTransfer.setData("application/reactflow", nodeType);
    event.dataTransfer.setData("application/reactflow2", label);
    event.dataTransfer.effectAllowed = "move";
  };

  return (
    <aside>
      <div className="description">
        You can drag these nodes to the pane on the right.
      </div>
      <div
        className="dndnode input"
        onDragStart={(event) => onDragStart(event, "input" , "AWS CodeGuru (SAST)")}
        draggable
      >
        AWS CodeGuru (SAST)
      </div>
      <div
        className="dndnode"
        onDragStart={(event) => onDragStart(event, "default" , "OWASP ZAP (DAST)")}
        draggable
      >
        OWASP ZAP (DAST)
      </div>
      <div
        className="dndnode output"
        onDragStart={(event) => onDragStart(event, "output" , "Docker Image Scanner")}
        draggable
      >
        Docker Image Scanner
      </div>
    </aside>
  );
};

export default Sidebar