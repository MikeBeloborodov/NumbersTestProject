import React from 'react'

function App() {
  const [apiData, setApiData] = React.useState([])

  React.useEffect(() => {
    fetch("http://localhost:5000/orders")
      .then(res => res.json())
      .then(data => {
          setApiData(data)
      })
  }, [])
  return (
    <div>
      <p>{JSON.stringify(apiData)}</p>
    </div>
  );
}

export default App;
