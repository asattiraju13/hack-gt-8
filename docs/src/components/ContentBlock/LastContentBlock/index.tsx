import { Row, Col } from "antd";
import { withTranslation } from "react-i18next";
import { SvgIcon } from "../../../common/SvgIcon";
import { ContentBlockProps } from "../types";
import { Fade } from "react-awesome-reveal";
import {
  LeftContentSection,
  Content,
  ContentWrapper,
  ServiceWrapper,
  HeadingContent,
  MinTitle,
  MinPara,
  MemberName
} from "./styles";

const LeftContentBlock = ({
  icon,
  title,
  vector,
  content,
  section,
  t,
  id,
}: ContentBlockProps) => {
  return (
    <LeftContentSection>
      <Fade direction="left">
        <Row justify="space-between" align="middle" id={id}>
          <Col lg={1}>
              <SvgIcon src={vector} width="45px" height="700px" />
          </Col>
          <Col lg={11} md={11} sm={12} xs={24}>
            <Row justify="space-around">
              <Col justify-content="center">
                <img src="https://i.ibb.co/m4spzQL/1598847346496.jpg" alt="lol" width="200px" />
                <MemberName>Ojasw U.</MemberName>
              </Col>
              <Col justify-content="center">
                <img src="https://i.ibb.co/zGQWkhs/1634697927727.jpg" alt="lol" width="200px" />
                <MemberName>Abhinav S.</MemberName>
              </Col>
            </Row>
            <Row justify="space-around">
              <Col justify-content="center">
                <img src="https://i.ibb.co/YBBtdxJ/1631815438564.jpg" alt="lol" width="200px" />
                <MemberName>Yatharth B.</MemberName>
              </Col>
              <Col justify-content="center">
                <img src="https://i.ibb.co/sRSWyyF/1606146111571.jpg" alt="lol" width="200px" />
                <MemberName>Darshan K.</MemberName>
              </Col>
            </Row>
          </Col>
          <Col lg={11} md={11} sm={11} xs={24}>
            <ContentWrapper>
              <HeadingContent>{t(title)}</HeadingContent>
              <Content>{t(content)}</Content>
              <ServiceWrapper>
                <Row justify="space-between">
                  {typeof section === "object" &&
                    section.map((item: any, id: number) => {
                      return (
                        <Col key={id} span={11}>
                          <SvgIcon src={item.icon} width="60px" height="60px" />
                          <MinTitle>{t(item.title)}</MinTitle>
                          <MinPara>{t(item.content)}</MinPara>
                        </Col>
                      );
                    })}
                </Row>
              </ServiceWrapper>
            </ContentWrapper>
          </Col>
        </Row>
      </Fade>
    </LeftContentSection>
  );
};

export default withTranslation()(LeftContentBlock);
