import React, { useState, useRef } from 'react';
import ReactFlow, {
  ReactFlowProvider,
  addEdge,
  removeElements,
  Controls,
} from 'react-flow-renderer';

import Sidebar from './Sidebar';

import '../css/dnd.css';

const initialElements = [
  {
    id: '1',
    type: 'input',
    sourcePosition: 'right',
    data: { label: 'Code Commit' },
    position: { x: 250, y: 100 },
  },
  {
    id: '2',
    sourcePosition: 'right',
    targetPosition: 'left',
    data: { label: 'Build' },
    position: { x: 500, y: 100 },
  },
  {
    id: '3',
    type: 'input',
    sourcePosition: 'left',
    data: { label: 'Deploy' },
    position: { x: 750, y: 100 },
  },
  
  {
    id: 'e1-2',
    source: '1',
    type: 'smoothstep',
    target: '2',
    animated: true,
  },
  {
    id: 'e2-3',
    source: '2',
    type: 'smoothstep',
    target: '3',
    animated: true,
  },
];

let id = 3;
const getId = () => `dndnode_${id++}`;

const FlowChart = () => {
  const reactFlowWrapper = useRef(null);
  const [reactFlowInstance, setReactFlowInstance] = useState(null);
  const [elements, setElements] = useState(initialElements);
  const onConnect = (params) => setElements((els) => addEdge(params, els));
  const onElementsRemove = (elementsToRemove) =>
    setElements((els) => removeElements(elementsToRemove, els));

  const onLoad = (_reactFlowInstance) =>
    setReactFlowInstance(_reactFlowInstance);

  const onDragOver = (event) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  };
  const graphStyles = { width: "100%", height: "500px" };
  const onDrop = (event) => {
    event.preventDefault();

    const reactFlowBounds = reactFlowWrapper.current.getBoundingClientRect();
    const type = event.dataTransfer.getData('application/reactflow');
    const label = event.dataTransfer.getData('application/reactflow2');
    const position = reactFlowInstance.project({
      x: event.clientX - reactFlowBounds.left,
      y: event.clientY - reactFlowBounds.top,
    });
    const newNode = {
      id: getId(),
      type,
      position,
      data: { label: label },
    };

    setElements((es) => es.concat(newNode));
  };

  return (
    <div className="dndflow">
      {console.log(elements.length)}
      <ReactFlowProvider>
        <div className="reactflow-wrapper" ref={reactFlowWrapper}>
          <ReactFlow
            elements={elements}
            onConnect={onConnect}
            onElementsRemove={onElementsRemove}
            onLoad={onLoad}
            onDrop={onDrop}
            onDragOver={onDragOver}
            style={graphStyles}
          >
            <Controls />
          </ReactFlow>
        </div>
        <Sidebar />
      </ReactFlowProvider>
    </div>
  );
};

export default FlowChart;