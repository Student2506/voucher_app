import { configureStore } from '@reduxjs/toolkit';
import userSlice from "./userSlice";
import ordersSlice from "./ordersSlice";
import changeDateSlice from "./changeDateSlice";

const store = configureStore({
  reducer: {
    changeDate: changeDateSlice,
    orders: ordersSlice,
    user: userSlice,
  }
})

export default store;
