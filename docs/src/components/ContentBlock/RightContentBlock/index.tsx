import { Row, Col } from "antd";
import { withTranslation } from "react-i18next";
import { SvgIcon } from "../../../common/SvgIcon";
import { Button } from "../../../common/Button";
import { ContentBlockProps } from "../types";
import { Fade } from "react-awesome-reveal";
import {
  RightBlockContainer,
  Content,
  ContentWrapper,
  ButtonWrapper,
  HeadingContent,
  WindowContainer
} from "./styles";

const RightBlock = ({
  title,
  content,
  button,
  icon,
  vector,
  t,
  id,
}: ContentBlockProps) => {
  const scrollTo = (id: string) => {
    const element = document.getElementById(id) as HTMLDivElement;
    element.scrollIntoView({
      behavior: "smooth",
    });
  };
  return (
    <WindowContainer>
      <RightBlockContainer>
        <Fade direction="right">
          <Row justify="end" align="middle" id={id}>
            <Col lg={12} md={12} sm={12} xs={20}>
              <ContentWrapper>
                <HeadingContent>{t(title)}</HeadingContent>
                <Content>{t(content)}</Content>
                <ButtonWrapper>
                  {typeof button === "object" &&
                    button.map((item: any, id: number) => {
                      return (
                        <Button
                          key={id}
                          color={item.color}
                          fixedWidth={true}
                          onClick={() => scrollTo("about")}
                        >
                          {t(item.title)}
                        </Button>
                      );
                    })}
                </ButtonWrapper>
              </ContentWrapper>
            </Col>
            <Col lg={7} md={7} sm={8} xs={16}>
              <SvgIcon src={icon} width="500px" height="500px" />
            </Col>
            <Col lg={3}>
              <SvgIcon src={vector} width="350px" height="570px" />
            </Col>
          </Row>
        </Fade>
      </RightBlockContainer>
    </WindowContainer>

  );
};

export default withTranslation()(RightBlock);
