import React from 'react';
import PropTypes from 'prop-types';
import Button from '@mui/material/Button';

const BigButton = (props: any) => {
  return (
    <Button
      sx={{ fontSize: '12pt' }}
      onClick={props.onClick}
      value={props.value}
      variant="outlined"
    >
      {props.children}
    </Button>
  );
};

export default BigButton;
BigButton.propTypes = {
  onClick: PropTypes.func,
  value: PropTypes.object,
  children: PropTypes.object,
};
