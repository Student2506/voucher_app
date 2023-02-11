/*
* Где используется React.memo это предотвращение лишнего ререндера компонента
* в useState хранятся данные о Customers его заказах и шаблонах
* Временно использую loggedIn как имитацию входа
*/

import './App.css';
import React, { useCallback, useEffect, useState } from 'react';
import { Route, Switch, useHistory } from "react-router-dom";
import Sign from "./components/Sign/Sign";
import Main from "./components/Main/Main";
import Api from "./utils/Api/Api";
import ProtectedRoute from "./components/ProtectedRoute/ProtectedRoute";
import LoadingScreen from "./components/LoadingScreen/LoadingScreen";
import useSuccess from "./hooks/useSuccess";

function App() {
  const [customers, setCustomers] = useState([]);
  const [customerOrders, setCustomerOrders] = useState([]);
  const [orderTemplates, setOrderTemplates] = useState([]);
  const [preload, setPreload] = useState(false);
  const [loadingScreen, setLoadingScreen] = useState(false);
  const [loggedIn, setLoggedIn] = useState(false);
  const history = useHistory();

  const {handleSwitchSuccess, handleClearErrors, success} = useSuccess();

  /*
  * Убираем лишнее обращение.
  * сработает только если юзер залогинился
  */
  useEffect(() => {
    if (loggedIn) {
      setLoadingScreen(true);
      Api.getCostumers().then((res) => {
        setCustomers(res.results);
      }).catch((err) => {console.log(err)}).finally(() => {setLoadingScreen(false)})
    } else {
      // Роутинг на вход
      history.push("/sign-in");
    }
  }, [loggedIn])

  function handleLogIn() {
    setLoggedIn(true);
    history.push('/vouchers');
  }

  /*
  * Убираем ререндер ссылки на функцию
  */
  const handleSelectCustomer = useCallback((id) => {
    Api.getCustomerOrders(id).then((res) => {
      setCustomerOrders(res.orders);
    }).catch((err) => {console.log(err)})
  }, []);

  const clearTemplates = useCallback(() => {
    setOrderTemplates([]);
    handleClearErrors();
  }, []);

  function handleSelectOrder(orderId) {
    Api.getOrderTemplates(orderId).then((res) => {
      /*Перевожу объект с key:value в массив объектов*/
      setOrderTemplates(Object.entries(res.templates).map((e) => ( { [e[0]]: e[1] } )));
    }).catch((err) => {console.log(err)})
  }

  function pushVocuher(id, template, email) {
    setPreload(true);
    Api.pushVouchers(id, template, email)
      .then((res) => {handleSwitchSuccess("templateSection", true)})
      .catch((err) => {handleSwitchSuccess("templateSection", false)})
      .finally(() => {setPreload(false)})
  }

  return (
    <>
      {loadingScreen ? <LoadingScreen /> : <></>}
      <Switch>
        {/*
      * Защищенный роут, если пользователь не залогинен - дальше не пропустит
      * И будет редиректить на /sign-in
      */}
        <ProtectedRoute
          component={Main}
          path={"/vouchers"}
          customersData={customers}
          onSelectCustomer={handleSelectCustomer}
          onSelectOrder={handleSelectOrder}
          customerOrders={customerOrders}
          orderTemplates={orderTemplates}
          onClear={clearTemplates}
          onSubmit={pushVocuher}
          loggedIn={loggedIn}
          preload={preload}
          success={success}
        />
        <Route path="/sign-in">
          <Sign onSubmit={handleLogIn} preload={preload} />
        </Route>
      </Switch>
    </>
  );
}

export default App;
