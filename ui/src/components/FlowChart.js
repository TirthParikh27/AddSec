import React, { useState, useRef } from "react";
import ReactFlow, {
  ReactFlowProvider,
  addEdge,
  removeElements,
  Controls,
} from "react-flow-renderer";

import Button from "@material-ui/core/Button";
import Sidebar from "./Sidebar";

import "../css/dnd.css";
import { Card, CardContent, Grid } from "@material-ui/core";
import SecurityIcon from "@material-ui/icons/Security";

const initialElements = [
  {
    id: "1",
    type: "input",
    sourcePosition: "right",
    data: { label: "Code Commit" },
    position: { x: 250, y: 100 },
  },
  {
    id: "2",
    sourcePosition: "right",
    targetPosition: "left",
    data: { label: "Build" },
    position: { x: 500, y: 100 },
  },
  {
    id: "3",
    type: "input",
    sourcePosition: "left",
    data: { label: "Deploy" },
    position: { x: 750, y: 100 },
  },

  {
    id: "e1-2",
    source: "1",
    type: "smoothstep",
    target: "2",
    animated: true,
  },
  {
    id: "e2-3",
    source: "2",
    type: "smoothstep",
    target: "3",
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

  const getElements = (list) => {
    var finalElements = [];
    var id = 1;
    var x = 250
    for (var i = 0; i < list.length; i++) {
      if (list[i]["visible"]) {
        if (finalElements.lenght === 0) {
          finalElements.append({
            id: String(id++),
            type: "input",
            sourcePosition: "right",
            data: { label: list[i]["name"] },
            position: { x: XPathEvaluator, y: 100 },
          });
        } else if (i === list.length - 1) {
          finalElements.append({
            id: String(id++),
            type: "input",
            sourcePosition: "left",
            data: { label: list[i]["name"] },
            position: { x: x, y: 100 },
          });
        } else {
          finalElements.append({
            id: String(id++),
            sourcePosition: "right",
            targetPosition: "left",
            data: { label: list[i]["name"] },
            position: { x: x, y: 100 },
          })
        }
        x += 250
      }
    }
    return finalElements
  };

  React.useEffect(() => {
    const fetchProducts = async () => {
      const products = await fetch("http://localhost:5000/getNamesPos").then((response)=>{
         return  response.json()
      }).then((data)=>{
        return data["steps"]
      })
      const finalElements = await getElements(products)
      setElements(finalElements)
    }
    fetchProducts()
  }, [])

  const onLoad = (_reactFlowInstance) => {
    _reactFlowInstance.fitView({ padding: 0.2 });
    setReactFlowInstance(_reactFlowInstance);
  };
  const handleIntegrate = () => {
    fetch("http://localhost:5000/secure", {
      method: "POST",
      body: elements,
    }).then((response) => {
      if (response.status == "200") {
        console.log("Succesfully Integrated !");
      } else {
        console.log("Integration Failed !");
      }
    });
  };
  const onDragOver = (event) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = "move";
  };
  const graphStyles = { width: "100%", height: "500px" };
  const onDrop = (event) => {
    event.preventDefault();

    const reactFlowBounds = reactFlowWrapper.current.getBoundingClientRect();
    const type = event.dataTransfer.getData("application/reactflow");
    const label = event.dataTransfer.getData("application/reactflow2");
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
        <Grid container alignItems="center" justify="center">
          <Grid item xs={10}>
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
          </Grid>
          <Grid item xs={2}>
            <Card style={{ height: "100%" }}>
              <CardContent>
                <Sidebar />
              </CardContent>
            </Card>
          </Grid>

          <Grid item={3}></Grid>
          <Grid item xs={6}>
            <Button
              startIcon={<SecurityIcon />}
              style={{
                backgroundColor: "#12824C",
                color: "#FFFFFF",
                width: "80%",
              }}
              variant="contained"
              onClick={handleIntegrate}
            >
              Intergate
            </Button>
          </Grid>
          <Grid item={3}></Grid>
        </Grid>
      </ReactFlowProvider>
    </div>
  );
};

export default FlowChart;
