import './App.css';
import React, { useEffect } from 'react';
import { Route, Switch, useHistory } from "react-router-dom";
import Sign from "./components/Sign/Sign";
import Main from "./components/Main/Main";
import ProtectedRoute from "./components/ProtectedRoute/ProtectedRoute";
import LoadingScreen from "./components/LoadingScreen/LoadingScreen";
import { useSelector, useDispatch } from "react-redux";
import { updateJwt } from "./utils/store/userSlice";
import { getCustomers } from "./utils/store/customersSlice";
import { NotFound } from "./components/NotFound/NotFound";
import { StatusPopup } from "./components/popups/StatusPopup/StatusPopup";
import { baseUrl } from "./constants";

function App() {
  const dispatch = useDispatch();
  const history = useHistory();
  const {loggedIn, userData} = useSelector(state => state.user);

  useEffect(() => {
    if (document.cookie) {
      const jwt = document.cookie.split('; ').reduce(function(result, v, i, a) { var k = v.split('='); result[k[0]] = k[1]; return result; }, {})
      if (!jwt.auth_refresh) {
        window.location.replace(`${baseUrl}/api/v1/oauth2/login`);
      } else {
        dispatch(updateJwt({jwtRefresh: jwt.auth_refresh}))
      }
    } else {
      window.location.replace(`${baseUrl}/api/v1/oauth2/login`);
    }
    // dispatch(updateJwt({jwtRefresh: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4MjE2NTQ1OSwianRpIjoiMTRjZDJiNzU0N2M0NDgxYjg4Nzc5MzIxNTBmODJmNDIiLCJ1c2VyX2lkIjoiYS52b2xvc2hpbiJ9.qrcSUB3q-rbeQ3eidR4tKNrgtz05ShwOFJkCJKpm_1U"}))
  }, [])

  useEffect(() => {
    if (loggedIn) {
      dispatch(getCustomers());
      history.push('/vouchers');
      /* Каждый 4 минуты обновляю jwt */
      setInterval(() => dispatch(updateJwt({jwtRefresh: userData.jwt.refr})), 240000);
    }
  }, [loggedIn])

  return (
    <>
      <StatusPopup />
      <Switch>
        {/*
      * Защищенный роут, если пользователь не залогинен - дальше не пропустит
      * И будет редиректить на /sign-in
      */}
        <ProtectedRoute
          component={Main}
          path={"/vouchers"}
          loggedIn={loggedIn}
        />
        <ProtectedRoute
          component={Main}
          path={"/refund"}
          loggedIn={loggedIn}
        />
        <ProtectedRoute
          component={Main}
          path={"/time-management"}
          loggedIn={loggedIn}
        />
        <Route path="/sign-in">
          <Sign />
        </Route>
        <Route path="*">
          <NotFound />
        </Route>
      </Switch>
    </>
  );
}

export default App;
