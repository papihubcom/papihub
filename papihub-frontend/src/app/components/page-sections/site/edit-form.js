"use client";
import FormProvider from "@/app/components/hook-form/form-provider";
import Select from "@/app/components/hook-form/select";
import {Controller, useForm} from "react-hook-form";
import Input from "@/app/components/hook-form/input";
import {RadioGroup} from "@headlessui/react";
import {CheckCircleIcon} from "@heroicons/react/24/solid";
import classNames from "classnames";
import {useAddSite, useListParsers} from "@/service/site-service";
import {useEffect, useState} from "react";
import * as Yup from "yup";
import {yupResolver} from "@hookform/resolvers/yup";
import Button from "@/app/components/button/button";
import {useRouter} from "next/navigation";

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
export default function SiteEditForm() {
  const router = useRouter();
  const {data} = useListParsers();
  const {mutate: addSite, isLoading} = useAddSite();
  const [siteOptions, setSiteOptions] = useState([]);
  useEffect(() => {
    setSiteOptions(data?.data?.map((item) => {
      return {
        icon: <img src={`/icons/pt/${item.site_id}.ico`} alt=""
                   className="h-5 w-5 flex-shrink-0 rounded-full"/>,
        label: item.site_name,
        value: item.site_id,
      }
    }) || []);
  }, [data]);
  const formSchema = Yup.object().shape({
    authType: Yup.string(),
    cookies: Yup.string()
    .when('authType', ([authType], schema) =>
        authType === 'cookies' ? schema.required('请填写一个有效的Cookies')
            : schema,
    ),
    username: Yup.string()
    .when('authType', ([authType], schema) =>
        authType === 'user_auth' ? schema.required('用户名必填') : schema,
    ),
    password: Yup.string()
    .when('authType', ([authType], schema) =>
        authType === 'user_auth' ? schema.required('密码必填') : schema,
    ),
  });
  const methods = useForm({
    resolver: yupResolver(formSchema),
    defaultValues: {
      authType: authOptions[0].value
    }
  });
  const {
    setValue,
    watch,
    control,
    register,
    handleSubmit,
    formState: {isSubmitting},
  } = methods;
  const authType = watch("authType");
  const onSubmit = handleSubmit(async (data) => {
    const params = {
      site_id: data.siteId.value,
      auth_type: data.authType,
      auth_config: data.authType === "cookies" ? {
        cookies: data.cookies
      } : {
        username: data.username,
        password: data.password
      }
    };
    console.log(params)
    addSite(params, {
      onSuccess: res => {
        const {success, message, data} = res;
        if (success) {
          //todo 提示成功
          router.push("/site");
        } else {
          //todo 提示失败
        }
      }
    });
  });
  useEffect(() => {
    if (siteOptions && siteOptions.length > 0) {
      setValue("siteId", siteOptions[0])
    }
  }, [siteOptions])
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
                                                  : 'border-white/10',
                                              'relative flex cursor-pointer rounded-lg border bg-white/5 p-4 shadow-sm focus:outline-none'
                                          )
                                      }
                                  >
                                    {({checked, active}) => (
                                        <>
                <span className="flex flex-1">
                  <span className="flex flex-col">
                    <RadioGroup.Label as="span"
                                      className="block text-sm font-medium text-white">
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
          <Button type="submit" disabled={isLoading}>
            立即添加
          </Button>
        </div>
      </FormProvider>)
}