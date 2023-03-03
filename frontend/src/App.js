/*
* Где используется React.memo это предотвращение лишнего ререндера компонента
* в useState хранятся данные о Customers его заказах и шаблонах
* Временно использую loggedIn как имитацию входа
*/

import './App.css';
import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { Route, Switch, useHistory } from "react-router-dom";
import Sign from "./components/Sign/Sign";
import Main from "./components/Main/Main";
import Api from "./utils/Api/Api";
import ProtectedRoute from "./components/ProtectedRoute/ProtectedRoute";
import LoadingScreen from "./components/LoadingScreen/LoadingScreen";
import useSuccess from "./hooks/useSuccess";
import { useSelector, useDispatch } from "react-redux";
import { updateJwt } from "./store/userSlice";
import { getCustomers } from "./store/customersSlice";

function App() {
  // const [customers, setCustomers] = useState([]);
  // const [customerOrders, setCustomerOrders] = useState([]);
  // const [orderTemplates, setOrderTemplates] = useState([]);
  const [preload, setPreload] = useState(false);
  const [loadingScreen, setLoadingScreen] = useState(false);

  const dispatch = useDispatch();
  const history = useHistory();

  const {handleSwitchSuccess, handleClearErrors, success} = useSuccess();

  const {loggedIn, userData} = useSelector(state => state.user);

  /*
  * Убираем лишнее обращение.
  * сработает только если юзер залогинился
  */

  useEffect(() => {
    if (document.cookie) {
      const jwt = document.cookie.split('; ').reduce(function(result, v, i, a) { var k = v.split('='); result[k[0]] = k[1]; return result; }, {})
      dispatch(updateJwt({jwtRefresh: jwt.auth_refresh}))
    }
  }, [])

  useEffect(() => {
    if (loggedIn) {
      dispatch(getCustomers(userData.jwt.auth));
      history.push('/vouchers');
      /* Каждый 4 минуты обновляю jwt */
      setInterval(() => dispatch(updateJwt({jwtRefresh: userData.jwt.refr})), 24000);
    } else {
      // Роутинг на вход
      history.push("/sign-in");
    }
  }, [loggedIn])

  /*
  * Убираем ререндер ссылки на функцию
  */
  // const handleSelectCustomer = (id) => {
  //   Api.getCustomerOrders(id, userData.jwt.auth).then((res) => {
  //     setCustomerOrders(res.orders);
  //   }).catch((err) => {console.log(err)})
  // }
  //
  // const clearTemplates = useCallback(() => {
  //   setOrderTemplates([]);
  //   handleClearErrors();
  // }, []);
  //
  // function handleSelectOrder(orderId) {
  //   Api.getOrderTemplates(orderId, userData.jwt.auth).then((res) => {
  //     /*Перевожу объект с key:value в массив объектов*/
  //     setOrderTemplates(Object.entries(res.templates).map((e) => ( { [e[0]]: e[1] } )));
  //   }).catch((err) => {console.log(err)})
  // }

  // function pushVoucher(id, template, email) {
  //   setPreload(true);
  //   Api.pushVouchers(id, template, email, userData.jwt.auth)
  //     .then((res) => {handleSwitchSuccess("templateSection", true)})
  //     .catch((err) => {handleSwitchSuccess("templateSection", false)})
  //     .finally(() => {setPreload(false)})
  // }

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
          // customersData={customers}
          // onSelectCustomer={handleSelectCustomer}
          // onSelectOrder={handleSelectOrder}
          // customerOrders={customerOrders}
          // orderTemplates={orderTemplates}
          // onClear={clearTemplates}
          // onSubmit={pushVoucher}
          loggedIn={loggedIn}
          preload={preload}
          success={success}
        />
        <Route path="/sign-in">
          <Sign preload={preload} />
        </Route>
      </Switch>
    </>
  );
}

export default App;
