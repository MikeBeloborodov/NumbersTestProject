import React from 'react'

function App() {
  const [tableElements, setTableElements] = React.useState([])
  const [refreshToggle, setRefreshToggle] = React.useState(false)

  React.useEffect(() => {
    fetch("http://localhost:5000/orders")
      .then(res => res.json())
      .then(data => {
          const elements = data.map(data => {
            return (
              <tr key={data.order_table_num}>
                <td>{data.order_table_num}</td>
                <td>{data.order_num}</td>
                <td>{data.price_rub}</td>
                <td>{data.price_usd}</td>
                <td>{data.delivery_date}</td>
              </tr>
            )
          })
          setTableElements(elements)
      })
  }, [refreshToggle])

  function handle_refresh_toggle(e){
    setRefreshToggle(oldValue => !oldValue)
  }

  return (
    <div className="container-md mt-5 mb-5">
      <div style={{display: "flex", justifyContent: "space-between"}}>
        <div></div>
        <button 
        className="btn btn-dark mb-3"
        onClick={e => {handle_refresh_toggle(e)}}
        >Обновить</button>
      </div>
      <table className="table table-bordered">
        <thead className="table-dark">
          <tr>
            <th scope="col">#</th>
            <th scope="col">Заказ №</th>
            <th scope="col">Стоимость, руб.</th>
            <th scope="col">Стоимость, $</th>
            <th scope="col">Срок поставки</th>
          </tr>
        </thead>
        <tbody className="table-light">
          {tableElements}
        </tbody>
      </table>
    </div>
  );
}

export default App;
