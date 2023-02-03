import './App.css';
import React, { useEffect, useState } from 'react';
import { Route, Switch, useHistory } from "react-router-dom";
import Sign from "./components/Sign/Sign";
import Main from "./components/Main/Main";
import Api from "./components/utils/Api/Api";

function App() {

  const [customers, setCustomers] = useState([]);
  const [customerOrders, setCustomerOrders] = useState([]);
  const [orderTemplates, setOrderTemplates] = useState([]);
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
    Api.getCustomerOrders(id).then((res) => {
      setCustomerOrders(res.orders);
    }).catch((err) => {console.log(err)})
  }

  function handleSelectOrder(orderId) {
    Api.getOrderTemplates(orderId).then((res) => {
      /*Перевожу объект с key:value в массив объектов*/
      setOrderTemplates(Object.entries(res.templates).map((e) => ( { [e[0]]: e[1] } )));
    }).catch((err) => {console.log(err)})
  }

  function pushVocuher(id, template, email) {
    Api.pushVouchers(id, template, email).then((res) => {console.log('ЕБОЙ')}).catch((err) => {console.log(err)})
  }

  function clearTemplates() {
    setOrderTemplates([]);
  }

  return (
    <Switch>
      <Route path="/sign-in">
        <Sign onSubmit={handleLogIn} />
      </Route>
      <Route path="/vouchers">
        <Main
          customersData={customers}
          onSelectCustomer={handleSelectCustomer}
          onSelectOrder={handleSelectOrder}
          customerOrders={customerOrders}
          orderTemplates={orderTemplates}
          onClear={clearTemplates}
          onSubmit={pushVocuher}
        />
      </Route>
    </Switch>
  );
}

export default App;
