import { configureStore } from '@reduxjs/toolkit';
import userSlice from "./userSlice";
import ordersSlice from "./ordersSlice";
import changeDateSlice from "./changeDateSlice";
import templatesSlice from "./templatesSlice";

const store = configureStore({
  reducer: {
    changeDate: changeDateSlice,
    orders: ordersSlice,
    user: userSlice,
    templates: templatesSlice,
  }
})

export default store;
