"use client";
import PropTypes from 'prop-types';
import {FormProvider as Form} from 'react-hook-form';

export default function FormProvider({
  className,
  children,
  onSubmit,
  methods
}) {
  return (
      <Form {...methods}>
        <form className={className} onSubmit={onSubmit}>{children}</form>
      </Form>
  );
}

FormProvider.propTypes = {
  className: PropTypes.string,
  children: PropTypes.node,
  methods: PropTypes.object,
  onSubmit: PropTypes.func,
};
