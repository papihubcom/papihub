"use client";
import PropTypes from 'prop-types';
import {Controller, useFormContext} from 'react-hook-form';
import classNames from "classnames";
import {ExclamationCircleIcon} from "@heroicons/react/20/solid";

// ----------------------------------------------------------------------

export default function Input({
  label,
  name,
  helperText,
  cornerHint,
  type,
  className,
  ...other
}) {
  const {control} = useFormContext();

  return (
      <Controller
          name={name}
          control={control}
          render={({field, fieldState: {error}}) => (
              <div className={"w-full"}>
                <div className="flex items-center justify-between">
                  <label htmlFor={name}
                         className="block text-sm font-medium leading-6 text-white">
                    {label}
                  </label>
                  <div className="text-sm leading-6 text-gray-500">
                    {cornerHint}
                  </div>
                </div>
                <div className={
                  classNames(
                      "mt-2",
                      {"relative": error}
                  )
                }>
                  <input
                      {...field}
                      type={type}
                      className={
                        classNames(
                            "block rounded-md border-0 py-1.5 bg-white/5 shadow-sm ring-1 ring-inset focus:ring-2 focus:ring-inset sm:text-sm sm:leading-6",
                            error
                                ? "text-red-900 ring-red-300 placeholder:text-red-300 focus:ring-red-500"
                                : "text-white ring-white/10 focus:ring-indigo-500",
                            className
                        )
                      }
                      value={type === 'number' && field.value === 0 ? ''
                          : field.value}
                      onChange={(event) => {
                        if (type === 'number') {
                          field.onChange(Number(event.target.value));
                        } else {
                          field.onChange(event.target.value);
                        }
                      }}
                      {...other}
                  />
                  {error && <div
                      className="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-3">
                    <ExclamationCircleIcon className="h-5 w-5 text-red-500"
                                           aria-hidden="true"/>
                  </div>}
                </div>
                {(helperText || error) && <p className={classNames(
                    "mt-2 text-sm",
                    error ? "text-red-500" : "text-gray-500"
                )}
                                             id="email-description">
                  {error ? error?.message : helperText}
                </p>}
              </div>
          )}
      />
  );
}

Input.propTypes = {
  label: PropTypes.string,
  cornerHint: PropTypes.object,
  helperText: PropTypes.object,
  name: PropTypes.string,
  type: PropTypes.string,
};
