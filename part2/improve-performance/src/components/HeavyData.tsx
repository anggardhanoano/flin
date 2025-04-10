import React, { useEffect, useState, useMemo } from "react";
import { FixedSizeGrid as Grid } from "react-window";

const heavyData = Array.from({ length: 100000 }, (_, i) => ({
  id: i,
  name: `Item ${i}`,
  value: Math.random() * 1000,
  description: `This is a long description for item ${i}`,
}));

const HeavyData = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [data, setData] = useState<any[]>([]);

  const result = useMemo(() => {
    return heavyData
      .filter((item) => item.value > 500)
      .map((item) => ({
        ...item,
        calculated: item.value * Math.random() * 10,
      }));
  }, []);

  useEffect(() => {
    // Simulate data fetching
    const timeout = setTimeout(() => {
      setData(result);
      setIsLoading(false);
    }, 1000);
    return () => clearTimeout(timeout);
  }, [result]);

  const columnCount = 3;
  const rowCount = Math.ceil(data.length / columnCount);
  const columnWidth = 250;
  const rowHeight = 150;

  const CellRenderer = ({
    columnIndex,
    rowIndex,
    style,
  }: {
    columnIndex: number;
    rowIndex: number;
    style: React.CSSProperties;
  }) => {
    const itemIndex = rowIndex * columnCount + columnIndex;
    if (itemIndex >= data.length) return null;

    const item = data[itemIndex];
    return (
      <div
        style={{
          ...style,
          padding: "10px",
          boxSizing: "border-box",
        }}
        className="data-item"
      >
        <h3>{item.name}</h3>
        <p>{item.description}</p>
        <span>{item.calculated.toFixed(2)}</span>
      </div>
    );
  };

  if (isLoading) {
    return <div className="heavy-content">Loading data...</div>;
  }

  return (
    <div className="heavy-content">
      {data.length > 0 && (
        <div>
          <h2>A Lot of Data</h2>
          <Grid
            className="data-grid"
            height={600}
            width={columnWidth * columnCount}
            columnCount={columnCount}
            columnWidth={columnWidth}
            rowCount={rowCount}
            rowHeight={rowHeight}
          >
            {CellRenderer}
          </Grid>
        </div>
      )}
    </div>
  );
};

export default HeavyData;
