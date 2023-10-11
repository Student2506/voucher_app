import './styles/app.scss';
import './styles/button.scss';
import Header from "./components/Header/Header";
import Navbar from "./components/Navbar/Navbar";
import { Route, Switch, useHistory } from "react-router-dom";
import Vouchers from "./components/pages/Vouchers/Vouchers";
import ChangeDateVouchers from "./components/pages/ChangeDateVouchers/ChangeDateVouchers";
import { useEffect, useMemo } from "react";
import { useDispatch, useSelector } from "react-redux";
import { updateJwt } from "./utils/store/userSlice";
import { BASE_URL } from "./constants";
import ProtectedRoute from "./components/ProtectedRoute/ProtectedRoute";
import NotFound from "./components/NotFound/NotFound";
import Refund from "./components/pages/Refund/Refund";
import SignIn from "./components/SignIn/SignIn";
import CreateTemplate from "./components/pages/CreateTemplate/CreateTemplate";

function App() {

  const dispatch = useDispatch();
  const { userData, loggedIn } = useSelector(state => state.user);
  const history = useHistory();

  // useEffect(() => {
  //   dispatch(updateJwt({jwtRefresh:
  //       "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY5MDM1NTk2NiwianRpIjoiYWI3OTI1NWNhZWIyNGM2M2IxYjFlOWVlMjAzNjFkMmEiLCJ1c2VyX2lkIjoiYS52b2xvc2hpbiJ9.NVRi6gsjc5k4lc_-nkBThyKRgE99j8rbOjq7axtTomc"
  //   }))
  // }, [])
  //
  // useEffect(() => {
  //   if (loggedIn) {
  //     console.log(userData.jwt.auth);
  //     setInterval(() => dispatch(updateJwt({jwtRefresh: userData.jwt.refr})), 240000);
  //   }
  // }, [loggedIn])

  useEffect(() => {
    if (document.cookie) {
      const jwt = document.cookie.split('; ').reduce(function(result, v, i, a) { var k = v.split('='); result[k[0]] = k[1]; return result; }, {})
      if (!jwt.auth_refresh) {
        window.location.replace(`${BASE_URL}/api/v1/oauth2/login`);
      } else {
        dispatch(updateJwt({jwtRefresh: jwt.auth_refresh}))
      }
    } else {
      window.location.replace(`${BASE_URL}/api/v1/oauth2/login`);
    }
    if (userData.jwt) {
      dispatch(updateJwt({jwtRefresh: userData.jwt.refr}))
    }
  }, [])

  useEffect(() => {
    if (loggedIn) {
      history.push("/vouchers");
      /* Каждый 4 минуты обновляю jwt */
      setInterval(() => dispatch(updateJwt({jwtRefresh: userData.jwt.refr})), 240000);
    }
  }, [loggedIn])

  return (
    <>
      <Header />
      <Navbar />
      <main className={"main"}>
        <Switch>
          <ProtectedRoute
            component={Vouchers}
            path={"/vouchers"}
            loggedIn={loggedIn}
          />
          <ProtectedRoute
            component={ChangeDateVouchers}
            path={"/change"}
            loggedIn={loggedIn}
          />
          <ProtectedRoute
            component={Refund}
            path={"/refund"}
            loggedIn={loggedIn}
          />
          <ProtectedRoute
            component={CreateTemplate}
            path={"/template"}
            loggedIn={loggedIn}
          />
          <Route path={"/sign-in"}>
            <SignIn />
          </Route>
          <Route path={"*"}>
            <NotFound text={"Упс... Похоже такой страницы не существует :("}/>
          </Route>
        </Switch>
      </main>
    </>
  );
}

export default App;
