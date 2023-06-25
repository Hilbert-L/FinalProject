import PropTypes from 'prop-types';

export interface RegistrationFormField {
  placeholder: string;
  value: string;
  inputType: string;
  onChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
}

export interface LoginFormField {
  placeholder: string;
  value: string;
  inputType: string;
  onChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
}
