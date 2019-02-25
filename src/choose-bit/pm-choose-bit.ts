/* global HTMLElement, customElements, MEDIA_PATH */
declare const MEDIA_PATH: string;

import { html, render } from "lit-html";
import { repeat } from "lit-html/directives/repeat";

import userDetailsService from "../site/user-details.service";
import "./choose-bit.css";
import { chooseBitService } from "./choose-bit.service";

interface TemplateData {
  isLoading: boolean;
  isReloading: boolean;
  hasError: boolean;
  message: string;
  limit: number;
  bits: string[];
  dots: number;
}

const minimumDotsRequired = 1400;
const limitBits = 10;

const tag = "pm-choose-bit";
let lastInstanceId = 0;

customElements.define(
  tag,
  class PmChooseBit extends HTMLElement {
    static get _instanceId(): string {
      return `${tag} ${lastInstanceId++}`;
    }
    private instanceId: string;

    static getBits(
      self: PmChooseBit,
      limit: number = limitBits
    ): Promise<void> {
      return chooseBitService
        .getBits(limit)
        .then((bits) => {
          self.bits = bits;
        })
        .catch(() => {
          self.hasError = true;
        })
        .finally(() => {
          self.isLoading = false;
          self.isReloading = false;
          self.render();
        });
    }

    private bits: string[] = Array(limitBits);
    private message: string = "";
    private limit: number;
    private isLoading: boolean = true;
    private isReloading: boolean = false;
    private hasError: boolean = false;

    constructor() {
      super();
      this.instanceId = PmChooseBit._instanceId;

      // Set the message from the message attribute
      const message = this.attributes.getNamedItem("message");
      this.message = message ? message.value : "";

      // Set the limit from the limit attribute
      const limit = this.attributes.getNamedItem("limit");
      this.limit = limit ? parseInt(limit.value) : limitBits;

      // need to get bits on the subscribe callback
      userDetailsService.subscribe(() => {
        if (userDetailsService.userDetails.dots > minimumDotsRequired) {
          PmChooseBit.getBits(this, this.limit);
        } else {
          this.render();
        }
      }, this.instanceId);

      //this.render();
    }

    handleClickMore() {
      this.isReloading = true;
      this.render();
      PmChooseBit.getBits(this, this.limit);
    }

    template(data: TemplateData) {
      const self = this;

      if (!(data.dots > minimumDotsRequired)) {
        return html`
          Insufficient dots to pick a different bit.
        `;
      }

      return html`
        <section class="pm-ChooseBit">
          <h1 class="pm-ChooseBit-message">
            ${data.message}
          </h1>
          <div class="pm-ChooseBit-items">
            ${items()}
          </div>
          <button
            ?disabled=${self.isReloading}
            @click=${self.handleClickMore.bind(self)}
          >
            More
          </button>
        </section>
      `;

      // During and after successfully loading the count of items should be
      // static.  Only show no items if there is an error or no bits are
      // available.
      function items() {
        if (data.isLoading) {
          return html`
            ${repeat(
              data.bits,
              (item) => item, // Key fn
              () => {
                return html`
                  <span class="pm-ChooseBit-item" role="list-item"></span>
                `;
              }
            )}
          `;
        }
        if (data.hasError) {
          return html`
            An error occured.
          `;
        } else {
          if (!data.bits.length) {
            return html`
              No bits are available at this time.
            `;
          } else {
            return html`
              ${repeat(
                data.bits,
                (item) => item, // Key fn
                (item) => {
                  return html`
                    <span class="pm-ChooseBit-item" role="list-item">
                      <button @click=${claimBit.bind(self)}>
                        <img
                          src="${MEDIA_PATH}bit-icons/64-${item}.png"
                          width="64"
                          height="64"
                          alt="${item}"
                        />
                      </button>
                    </span>
                  `;

                  function claimBit() {
                    chooseBitService.claimBit(item).then(() => {
                      const userDetailsChangeEvent = new Event(
                        "userDetailsChange",
                        {
                          bubbles: true,
                        }
                      );
                      self.dispatchEvent(userDetailsChangeEvent);
                    });
                  }
                }
              )}
            `;
          }
        }
      }
    }

    get data(): TemplateData {
      return {
        dots: userDetailsService.userDetails.dots,
        isLoading: this.isLoading,
        isReloading: this.isReloading,
        hasError: this.hasError,
        message: this.message,
        limit: this.limit,
        bits: this.bits,
      };
    }

    render() {
      render(this.template(this.data), this);
    }
  }
);
