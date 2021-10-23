import LeftContentBlock from "./LeftContentBlock";
import RightContentBlock from "./RightContentBlock";
import LastContentBlock from "./LastContentBlock";
import { ContentBlockProps } from "./types";

const ContentBlock = (props: ContentBlockProps) => {
  if (props.type === "left") return <LeftContentBlock {...props} />;
  if (props.type === "right") return <RightContentBlock {...props} />;
  if (props.type === "last") return <LastContentBlock {...props} />;
  return null;
};

export default ContentBlock;
