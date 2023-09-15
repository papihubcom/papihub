import {create} from "zustand";
import {setSession} from "@/auth/utils";
import axios from "@/utils/axios";

const useUserStore = create((set, get) => ({
  isInitializing: true,
  user: null,
  authenticated: false,
  hasError: false,
  errorMessage: null,
  initializeMethod: async () => {
    const accessToken = window.localStorage.getItem("accessToken");
    setSession(accessToken);
    try {
      const response = await axios.get("/api/user/profile");
      const {success, data} = response;
      if (success) {
        set({user: data, authenticated: true, isInitializing: false});
      } else {
        setSession(null)
        set({isInitializing: false});
      }
    } catch (e) {
      setSession(null);
      set({isInitializing: false});
    }
  },
  login: async (username, password) => {
    let formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);
    const response = await axios.post(
        "/api/user/get_token",
        formData
    );
    const {success, data, message} = response;
    if (success) {
      setSession(data.access_token);
      set({user: data.user, authenticated: true, isInitializing: true});
    } else {
      set({hasError: true, errorMessage: message});
    }
  },
  logout: () => {
    setSession(null);
    set({user: null, authenticated: false, isInitializing: true});
  }
}));

export default useUserStore;