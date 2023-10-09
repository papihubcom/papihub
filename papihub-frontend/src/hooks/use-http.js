import axios from "@/utils/axios";
import { useCallback } from 'react';

const useHttp = () => {
    return useCallback(
        (...[endpoint, config]) =>
            (config?.method?.toUpperCase() === "POST"
                ? axios.post(endpoint, config.params)
                : axios.get(endpoint, config)),
        []
    );
};

export default useHttp;

