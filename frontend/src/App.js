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

function App() {
  const dispatch = useDispatch();
  const history = useHistory();
  const {loggedIn, userData} = useSelector(state => state.user);
  const {error, status} = useSelector(state => state.status);

  useEffect(() => {
    if (document.cookie) {
      const jwt = document.cookie.split('; ').reduce(function(result, v, i, a) { var k = v.split('='); result[k[0]] = k[1]; return result; }, {})
      dispatch(updateJwt({jwtRefresh: jwt.auth_refresh}))
    } else {
      window.location.replace('https://adfs.karo-film.ru/adfs/oauth2/authorize/?response_type=code&client_id=c00aac15-160c-4b54-8301-35863f4fcab6&resource=c00aac15-160c-4b54-8301-35863f4fcab6&redirect_uri=http%3A%2F%2F10.0.10.234%2Fapi%2Fv1%2Foauth2%2Fcallback&state=cmV0cmlldmUtdG9rZW4%3D&scope=openid&prompt=login&client-request-id=92d81cb3-ddff-43be-6510-0080020000f5&pullStatus=0');
    }
  }, [])

  useEffect(() => {
    if (loggedIn) {
      dispatch(getCustomers(userData.jwt.auth));
      history.push('/vouchers');
      /* Каждый 4 минуты обновляю jwt */
      setInterval(() => dispatch(updateJwt({jwtRefresh: userData.jwt.refr})), 240000);
    } else {
      // Роутинг на вход
      history.push("/sign-in");
    }
  }, [loggedIn])

  return (
    <>
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
        <Route path="/sign-in">
          <Sign />
        </Route>
      </Switch>
    </>
  );
}

export default App;
