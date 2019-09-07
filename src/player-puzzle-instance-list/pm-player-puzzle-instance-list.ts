import { html, render } from "lit-html";
//import { classMap } from "lit-html/directives/class-map.js";
import userDetailsService from "../site/user-details.service";
import { PuzzleInstanceList } from "../site/user-details.service";
import "./player-puzzle-instance-list.css";

interface TemplateData {
  isReady: boolean;
  hasPuzzleInstanceList: boolean;
  puzzleInstanceList: PuzzleInstanceList;
  createPuzzleInstanceHref: string;
}

const tag = "pm-player-puzzle-instance-list";
let lastInstanceId = 0;

customElements.define(
  tag,
  class PmPlayerPuzzleInstanceList extends HTMLElement {
    static get _instanceId(): string {
      return `${tag} ${lastInstanceId++}`;
    }

    private instanceId: string;
    createPuzzleInstanceHref: string = "";
    start: number = 0;
    end: undefined | number = undefined;

    isReady: boolean = false;
    puzzleInstanceList: PuzzleInstanceList = [];

    constructor() {
      super();
      this.instanceId = PmPlayerPuzzleInstanceList._instanceId;

      // Set the attribute values
      const createPuzzleInstanceHref = this.attributes.getNamedItem(
        "create-puzzle-instance-href"
      );
      if (!createPuzzleInstanceHref || !createPuzzleInstanceHref.value) {
        throw new Error(
          "no create-puzzle-instance-href attribute has been set"
        );
      } else {
        this.createPuzzleInstanceHref = createPuzzleInstanceHref.value;
      }

      const end = this.attributes.getNamedItem("end");
      if (end && end.value) {
        this.end = parseInt(end.value);
      }
      const start = this.attributes.getNamedItem("start");
      if (start && start.value) {
        this.start = parseInt(start.value);
      }

      // TODO: support a size attribute so all the instances can be shown on the
      // profile page.

      userDetailsService.subscribe(
        this._setPuzzleInstanceList.bind(this),
        this.instanceId
      );
    }

    _setPuzzleInstanceList() {
      if (
        userDetailsService.userDetails.puzzle_instance_list &&
        userDetailsService.userDetails.puzzle_instance_list.length
      ) {
        if (this.end !== undefined) {
          this.puzzleInstanceList = userDetailsService.userDetails.puzzle_instance_list.slice(
            userDetailsService.userDetails.puzzle_instance_list.length -
              this.end,
            userDetailsService.userDetails.puzzle_instance_list.length -
              this.start
          );
        } else {
          this.puzzleInstanceList =
            userDetailsService.userDetails.puzzle_instance_list;
        }
      }
      this.isReady = true;
      this.render();
    }

    template(data: TemplateData) {
      if (!data.isReady || !data.hasPuzzleInstanceList) {
        return html``;
      }
      return html`
        <div class="pm-PlayerPuzzleInstanceList">
          <ul class="pm-PlayerPuzzleInstanceList-list">
            ${data.puzzleInstanceList.map(
              (puzzleInstanceItem) => html`
                <li class="pm-PlayerPuzzleInstanceList-listItem">
                  ${puzzleInstanceItem.front_url
                    ? html`
                        <a
                          class="pm-PlayerPuzzleInstanceList-instanceLink"
                          href=${puzzleInstanceItem.front_url}
                          title="player puzzle instance"
                        >
                          <img
                            width="30"
                            height="30"
                            src=${puzzleInstanceItem.src}
                            alt=""
                          />
                        </a>
                      `
                    : html`
                        <span class="pm-PlayerPuzzleInstanceList-add"></span>
                      `}
                </li>
              `
            )}
          </ul>
        </div>
      `;
    }

    get data(): TemplateData {
      return {
        isReady: this.isReady,
        hasPuzzleInstanceList: !!(
          this.puzzleInstanceList && this.puzzleInstanceList.length
        ),
        puzzleInstanceList: this.puzzleInstanceList,
        createPuzzleInstanceHref: this.createPuzzleInstanceHref,
      };
    }

    render() {
      render(this.template(this.data), this);
    }

    disconnectedCallback() {
      userDetailsService.unsubscribe(this.instanceId);
    }
  }
);