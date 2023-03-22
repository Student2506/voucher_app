import { configureStore } from '@reduxjs/toolkit';
import userSlice from "./userSlice";
import customersSlice from "./customersSlice";
import statusAppSlice from "./statusAppSlice";

const store = configureStore({
  reducer: {
    user: userSlice,
    customers: customersSlice,
    status: statusAppSlice,
  },
})

export default store;
