import { configureStore, combineReducers } from '@reduxjs/toolkit';
import { persistStore, persistReducer, FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER } from 'redux-persist' // imports from redux-persist
import storage from 'redux-persist/lib/storage'
import userSlice from "./userSlice";

// const rootReducer = combineReducers({
//   user: userSlice,
// })
//
// const persistConfig = {
//   key: 'user',
//   storage,
// }
//
// const persistedReducer = persistReducer(persistConfig, rootReducer)

const store = configureStore({
  reducer: {
    user: userSlice,
  },
})

// export const persistor = persistStore(store);

export default store;
