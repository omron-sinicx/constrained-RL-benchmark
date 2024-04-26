import React from 'react';
import { render } from 'react-dom';

export default class Footer extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    return (
      <div className="uk-text-center uk-text-meta">
        <a href="https://www.omron.com/sinicx/" target="_blank">
          <h6>© 2024 OMRON SINIC X Corporation, all rights reserved.</h6>
        </a>
      </div>
    );
  }
}
