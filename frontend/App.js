import './App.css';
import React, { useEffect, useState } from 'react';
import { Route, Switch, useHistory } from "react-router-dom";
import Sign from "./components/Sign/Sign";
import Main from "./components/Main/Main";
import Api from "./components/utils/Api/Api";

function App() {

  const [customers, setCustomers] = useState([]);
  const [customerOrders, setCustomerOrders] = useState([]);
  const history = useHistory();

  useEffect(() => {
    Api.getCostumers().then((res) => {
      setCustomers(res.results);
    }).catch((err) => {console.log(err)})
  }, [])

  function handleLogIn() {
    history.push('/vouchers');
  }

  function handleSelectCustomer(id) {
    Api.getCustomerOrder(id).then((res) => {
      setCustomerOrders(res.orders);
    })
  }

  console.log(customers);
  console.log(customerOrders);

  return (
    <Switch>
      <Route path="/sign-in">
        <Sign onSubmit={handleLogIn} />
      </Route>
      <Route path="/vouchers">
        <Main customersData={customers} onSelectCustomer={handleSelectCustomer}/>
      </Route>
    </Switch>
  );
}

export default App;
