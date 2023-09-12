import {create} from "zustand";

const useUserStore = create((set, get) => ({
  user: null,
  authenticated: false,
  hasError: false,
  errorMessage: null,
}));

export default useUserStore;