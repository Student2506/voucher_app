import { configureStore } from '@reduxjs/toolkit';
import userSlice from "./userSlice";
import customersSlice from "./customersSlice";
import statusAppSlice from "./statusAppSlice";
import changeDateSlice from "./changeDateSlice";

const store = configureStore({
  reducer: {
    user: userSlice,
    customers: customersSlice,
    status: statusAppSlice,
    changeDate: changeDateSlice,
  },
})

export default store;
