"use client"
import {Fragment} from 'react'

import classNames from "classnames";
import {CheckIcon, ChevronUpDownIcon} from "@heroicons/react/24/solid";
import {Listbox, Transition} from "@headlessui/react";
import {Controller, useFormContext} from "react-hook-form";
import {ExclamationCircleIcon} from "@heroicons/react/20/solid";

export default function Select({
  name,
  label,
  cornerHint,
  options,
  helperText
}) {
  const {control} = useFormContext();

  return (
      <Controller
          name={name}
          control={control}
          render={({field, fieldState: {error}}) => (
              <div>
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
                  <Listbox value={field.value} onChange={field.onChange}>
                    {({open}) => (
                        <>
                          <div className="relative mt-2">
                            <Listbox.Button
                                className="relative w-full cursor-default rounded-md bg-white/5 py-1.5 pl-3 pr-10 text-left text-white shadow-sm ring-1 ring-inset ring-white/10 focus:outline-none focus:ring-2 focus:ring-indigo-500 sm:text-sm sm:leading-6">
              <span className="flex items-center">
                {field.value?.icon}
                <span
                    className="ml-3 block truncate">{field.value?.label}</span>
              </span>
                              <span
                                  className="pointer-events-none absolute inset-y-0 right-0 ml-3 flex items-center pr-2">
                <ChevronUpDownIcon className="h-5 w-5 text-gray-400"
                                   aria-hidden="true"/>
              </span>
                            </Listbox.Button>
                            <Transition
                                show={open}
                                as={Fragment}
                                leave="transition ease-in duration-100"
                                leaveFrom="opacity-100"
                                leaveTo="opacity-0"
                            >
                              <Listbox.Options
                                  className="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                                {options.map((item, index) => (
                                    <Listbox.Option
                                        key={index}
                                        className={({active}) =>
                                            classNames(
                                                active
                                                    ? 'bg-indigo-600 text-white'
                                                    : 'text-gray-900',
                                                'relative cursor-default select-none py-2 pl-3 pr-9'
                                            )
                                        }
                                        value={item}
                                    >
                                      {({selected, active}) => (
                                          <>
                                            <div className="flex items-center">
                                              {item.icon}
                                              <span
                                                  className={classNames(
                                                      selected ? 'font-semibold'
                                                          : 'font-normal',
                                                      'ml-3 block truncate')}
                                              >
                            {item.label}
                          </span>
                                            </div>

                                            {selected ? (
                                                <span
                                                    className={classNames(
                                                        active ? 'text-white'
                                                            : 'text-indigo-600',
                                                        'absolute inset-y-0 right-0 flex items-center pr-4'
                                                    )}
                                                >
                            <CheckIcon className="h-5 w-5" aria-hidden="true"/>
                          </span>
                                            ) : null}
                                          </>
                                      )}
                                    </Listbox.Option>
                                ))}
                              </Listbox.Options>
                            </Transition>
                          </div>
                        </>
                    )}
                  </Listbox>{error && <div
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
  )
}