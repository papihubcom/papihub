"use client";
import FormProvider from "@/app/components/hook-form/form-provider";
import Select from "@/app/components/hook-form/select";
import {Controller, useForm} from "react-hook-form";
import Input from "@/app/components/hook-form/input";
import {RadioGroup} from "@headlessui/react";
import {CheckCircleIcon} from "@heroicons/react/24/solid";
import classNames from "classnames";

export default function SiteEditForm() {
  const siteOptions = [{label: "馒头", value: "mteam"}];
  const authOptions = [{
    id: 1,
    label: "Cookies认证",
    desc: "登录站点后，通过浏览器抓包获取。",
    value: "cookies"
  }, {
    id: 2,
    label: "登录认证",
    desc: "直接使用用户名密码认证，少量站点支持。",
    value: "user_auth"
  }];
  const methods = useForm({
    defaultValues: {
      siteId: siteOptions[0],
      authType: authOptions[0].value
    }
  });
  const {
    watch,
    control,
    register,
    handleSubmit,
    formState: {isSubmitting},
  } = methods;
  const authType = watch("authType");
  const onSubmit = handleSubmit(async (data) => {
    console.log(data)
  });
  return (
      <FormProvider methods={methods} onSubmit={onSubmit}>
        <div className="space-y-4">
          <div
              className="mt-10 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
            <div className="sm:col-span-4">
              <Select name={"siteId"} label={"选择站点"} options={siteOptions}/>
            </div>
          </div>

          <div className="border-b border-white/10 pb-12">
            <div className="mt-10 space-y-10">
              <Controller
                  name={"authType"}
                  control={control}
                  render={({field, fieldState: {error}}) => (

                      <RadioGroup value={field.value} onChange={field.onChange}>
                        <RadioGroup.Label
                            className="text-base font-semibold leading-6 text-white">
                          选择认证方式
                        </RadioGroup.Label>

                        <div
                            className="mt-4 grid grid-cols-1 gap-y-6 sm:grid-cols-3 sm:gap-x-4">
                          {authOptions.map(
                              (item) => (
                                  <RadioGroup.Option
                                      key={item.value}
                                      value={item.value}
                                      className={({active}) =>
                                          classNames(
                                              active
                                                  ? 'border-indigo-600 ring-2 ring-indigo-600'
                                                  : 'border-gray-300',
                                              'relative flex cursor-pointer rounded-lg border bg-white p-4 shadow-sm focus:outline-none'
                                          )
                                      }
                                  >
                                    {({checked, active}) => (
                                        <>
                <span className="flex flex-1">
                  <span className="flex flex-col">
                    <RadioGroup.Label as="span"
                                      className="block text-sm font-medium text-gray-900">
                      {item.label}
                    </RadioGroup.Label>
                    <RadioGroup.Description as="span"
                                            className="mt-1 flex items-center text-sm text-gray-500">
                      {item.desc}
                    </RadioGroup.Description>
                  </span>
                </span>
                                          <CheckCircleIcon
                                              className={classNames(
                                                  !checked ? 'invisible' : '',
                                                  'h-5 w-5 text-indigo-600')}
                                              aria-hidden="true"
                                          />
                                          <span
                                              className={classNames(
                                                  active ? 'border'
                                                      : 'border-2',
                                                  checked ? 'border-indigo-600'
                                                      : 'border-transparent',
                                                  'pointer-events-none absolute -inset-px rounded-lg'
                                              )}
                                              aria-hidden="true"
                                          />
                                        </>
                                    )}
                                  </RadioGroup.Option>
                              ))}
                        </div>
                      </RadioGroup>)}/>
              {authType === "cookies" && <fieldset>
                <div className="space-y-6">
                  <Input className={"w-full"} label={"Cookies"} name={"cookies"}
                         type={"text"}/>
                </div>
              </fieldset>}
              {authType === "user_auth" && <fieldset>
                <div className="flex flex-col space-y-3 w-2/3">
                  <Input className={"w-full"} label={"用户名"} name={"username"}
                         type={"text"}/>
                  <Input className={"w-full"} label={"密码"} name={"password"}
                         type={"password"}/>
                </div>
              </fieldset>}
            </div>
          </div>
        </div>

        <div className="mt-6 flex items-center justify-start gap-x-6">
          <button
              type="submit"
              className="rounded-md bg-indigo-500 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500"
          >
            立即添加
          </button>
        </div>
      </FormProvider>)
}